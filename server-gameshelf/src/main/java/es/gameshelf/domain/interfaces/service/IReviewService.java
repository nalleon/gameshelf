package es.gameshelf.domain.interfaces.service;

import es.gameshelf.domain.*;

import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * @author Nabil L. A. @nalleon
 */
public interface IReviewService {
    Review add(String content, User user, Game game, Set<PhotoReview> photoReviewSet);
    List<Review> findAll();
    List<Review> findAllByUser(User user);
    List<Review> findAllByGame(Game game);
    List<Review> findAllByUserLatest(User user);
    List<Review> findAllByGameLatest(Game game);

    int countAllGroupedByUser(User user);
    int countAllGroupedByGame(Game game);

    Review findById(Integer id);
    boolean delete(Integer id);
    Review update(Integer id, String content, User user, Game game, Set<PhotoReview> photoReviewSet);
}

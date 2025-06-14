package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.*;

import java.util.List;

public interface IGameRepository {
    Game save(Game game);
    List<Game> findAll();
    Game findById(Integer id);
    Game findByTitle(String title);
    Game findBySlug(String slug);

    List<Game> findAllByYear(Integer year);
    List<Game> findAllByPlatform(Platform platform);
    List<Game> findAllByDeveloper(Developer developer);
    List<Game> findAllByPublisher(Publisher publisher);
    List<Game> findAllByGenre(Genre genre);
    List<Game> findAllByFormat(Format format);

    List<Game> findAllByUserAlphabeticalOrder();
    List<Game> findAllByUserOldestOrder();
    List<Game> findAllByUserLatestOrder();

    boolean delete(Integer id);
    Game update(Game game);
}

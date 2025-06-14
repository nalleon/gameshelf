package es.gameshelf.domain.interfaces.repository;

import es.gameshelf.domain.Platform;

import java.util.List;
/**
 * @author Nabil L. A. @nalleon
 */
public interface IPlatformRepository {
    Platform save(Platform platform);
    List<Platform> findAll();
    Platform findById(Integer id);
    Platform findByName(String name);
    boolean delete(Integer id);
    Platform update(Platform platform);
}
